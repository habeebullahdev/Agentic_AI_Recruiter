import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings
from app.core.logging import logger
from app.schemas.rag import RAGResumeSearchResultItem, RAGJDSearchResultItem


class RAGService:
    """
    RAG (Retrieval-Augmented Generation) & Semantic Vector Search Service.
    Uses ChromaDB persistent vector database and Google Gemini Embeddings to enable:
      - Candidate Resume Semantic Search
      - Job Description Semantic Search
      - Multi-candidate Ranking & Semantic Context Retrieval
    """

    def __init__(self):
        os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)

        # Initialize collections
        self.resume_collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_RESUMES,
            metadata={"description": "Candidate resumes embeddings vector store"}
        )
        self.jd_collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_JDS,
            metadata={"description": "Job descriptions embeddings vector store"}
        )

        # Embeddings provider
        self.embeddings = None
        if settings.GEMINI_API_KEY:
            try:
                self.embeddings = GoogleGenerativeAIEmbeddings(
                    model=settings.GEMINI_EMBEDDING_MODEL,
                    google_api_key=settings.GEMINI_API_KEY
                )
            except Exception as e:
                logger.warning(f"Could not initialize GoogleGenerativeAIEmbeddings: {e}")

    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Generates dense vector embedding using Gemini or returns None for Chroma default."""
        if self.embeddings:
            try:
                return self.embeddings.embed_query(text)
            except Exception as e:
                logger.error(f"Error generating embedding via Google Generative AI: {e}")
        return None

    # ==========================================
    # Resume Indexing & Search
    # ==========================================

    def index_resume(
        self,
        resume_id: int,
        extracted_text: str,
        file_name: str,
        candidate_name: Optional[str] = None,
        skills: Optional[List[str]] = None
    ) -> None:
        """
        Indexes a resume into the ChromaDB vector database.
        """
        try:
            doc_id = f"resume_{resume_id}"
            metadata = {
                "resume_id": resume_id,
                "file_name": file_name,
                "candidate_name": candidate_name or "Unknown",
                "skills": ", ".join(skills or [])[:500],
            }

            embedding = self._get_embedding(extracted_text)
            if embedding:
                self.resume_collection.upsert(
                    ids=[doc_id],
                    documents=[extracted_text],
                    embeddings=[embedding],
                    metadatas=[metadata]
                )
            else:
                self.resume_collection.upsert(
                    ids=[doc_id],
                    documents=[extracted_text],
                    metadatas=[metadata]
                )
            logger.info(f"Successfully indexed resume ID {resume_id} into ChromaDB")
        except Exception as e:
            logger.error(f"Failed to index resume {resume_id} in ChromaDB: {e}", exc_info=True)

    def search_resumes(
        self,
        query: str,
        top_k: int = 5,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> List[RAGResumeSearchResultItem]:
        """
        Performs semantic vector search across all candidate resumes.
        """
        try:
            query_embedding = self._get_embedding(query)
            if query_embedding:
                results = self.resume_collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=where_filter
                )
            else:
                results = self.resume_collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where=where_filter
                )

            items = []
            if results and results["ids"] and len(results["ids"][0]) > 0:
                ids = results["ids"][0]
                docs = results["documents"][0] if results.get("documents") else []
                metadatas = results["metadatas"][0] if results.get("metadatas") else []
                distances = results["distances"][0] if results.get("distances") else []

                for i in range(len(ids)):
                    meta = metadatas[i] if i < len(metadatas) else {}
                    doc = docs[i] if i < len(docs) else ""
                    dist = distances[i] if i < len(distances) else 0.5
                    # Convert distance to similarity score
                    sim_score = round(max(0.0, 1.0 - (dist / 2.0)), 4) if dist is not None else 0.85
                    
                    skills_str = meta.get("skills", "")
                    skills_list = [s.strip() for s in skills_str.split(",") if s.strip()]

                    items.append(
                        RAGResumeSearchResultItem(
                            resume_id=int(meta.get("resume_id", 0)),
                            candidate_name=meta.get("candidate_name", "Candidate"),
                            similarity_score=sim_score,
                            snippet=doc[:300] + "..." if len(doc) > 300 else doc,
                            skills=skills_list,
                            metadata=meta
                        )
                    )
            return items
        except Exception as e:
            logger.error(f"Error during resume semantic search: {e}", exc_info=True)
            return []

    # ==========================================
    # Job Description Indexing & Search
    # ==========================================

    def index_jd(
        self,
        jd_id: int,
        title: str,
        jd_text: str,
        required_skills: Optional[List[str]] = None
    ) -> None:
        """
        Indexes a Job Description into ChromaDB vector store.
        """
        try:
            doc_id = f"jd_{jd_id}"
            metadata = {
                "jd_id": jd_id,
                "title": title,
                "required_skills": ", ".join(required_skills or [])[:500]
            }
            content = f"Job Title: {title}\nRequired Skills: {metadata['required_skills']}\nDescription:\n{jd_text}"

            embedding = self._get_embedding(content)
            if embedding:
                self.jd_collection.upsert(
                    ids=[doc_id],
                    documents=[content],
                    embeddings=[embedding],
                    metadatas=[metadata]
                )
            else:
                self.jd_collection.upsert(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[metadata]
                )
            logger.info(f"Successfully indexed Job Description ID {jd_id} into ChromaDB")
        except Exception as e:
            logger.error(f"Failed to index JD {jd_id} in ChromaDB: {e}", exc_info=True)

    def search_jds(self, query: str, top_k: int = 5) -> List[RAGJDSearchResultItem]:
        """
        Performs semantic vector search across all Job Descriptions.
        """
        try:
            query_embedding = self._get_embedding(query)
            if query_embedding:
                results = self.jd_collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k
                )
            else:
                results = self.jd_collection.query(
                    query_texts=[query],
                    n_results=top_k
                )

            items = []
            if results and results["ids"] and len(results["ids"][0]) > 0:
                ids = results["ids"][0]
                docs = results["documents"][0] if results.get("documents") else []
                metadatas = results["metadatas"][0] if results.get("metadatas") else []
                distances = results["distances"][0] if results.get("distances") else []

                for i in range(len(ids)):
                    meta = metadatas[i] if i < len(metadatas) else {}
                    doc = docs[i] if i < len(docs) else ""
                    dist = distances[i] if i < len(distances) else 0.5
                    sim_score = round(max(0.0, 1.0 - (dist / 2.0)), 4) if dist is not None else 0.85

                    items.append(
                        RAGJDSearchResultItem(
                            jd_id=int(meta.get("jd_id", 0)),
                            title=meta.get("title", "Job Title"),
                            similarity_score=sim_score,
                            snippet=doc[:300] + "..." if len(doc) > 300 else doc,
                            metadata=meta
                        )
                    )
            return items
        except Exception as e:
            logger.error(f"Error during JD semantic search: {e}", exc_info=True)
            return []

    def delete_resume_index(self, resume_id: int) -> None:
        try:
            self.resume_collection.delete(ids=[f"resume_{resume_id}"])
        except Exception as e:
            logger.warning(f"ChromaDB delete resume {resume_id} warning: {e}")

    def delete_jd_index(self, jd_id: int) -> None:
        try:
            self.jd_collection.delete(ids=[f"jd_{jd_id}"])
        except Exception as e:
            logger.warning(f"ChromaDB delete JD {jd_id} warning: {e}")


rag_service = RAGService()
