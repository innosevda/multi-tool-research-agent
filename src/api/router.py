from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.api.schema import PaperResponse
from src.database.database import get_db
from src.database.models import ResearchPaper
from src.services.summarizer import SummarizationError, summarize_pdf

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PAPER_STORAGE_DIR = PROJECT_ROOT / "research_papers"
MAX_FILE_SIZE = 50 * 1024 * 1024


@router.get("/health", status_code=200)
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "OK"}

@router.post("/paper", response_model=PaperResponse, status_code=201)
async def upload_paper(
    file: UploadFile = File(...),
    title: str = Form(..., min_length=1, max_length=200),
    author: str = Form(..., min_length=1, max_length=200),
    summary: str | None = Form(None, max_length=30000),
    db: Session = Depends(get_db),
) -> PaperResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    if await file.read(5) != b"%PDF-":
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF")
    await file.seek(0)

    title = title.strip()
    author = author.strip()
    summary = summary.strip() if summary else None
    if not title or not author:
        raise HTTPException(
            status_code=422,
            detail="Title and author are required",
        )

    PAPER_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    stored_path = PAPER_STORAGE_DIR / f"{uuid4().hex}.pdf"

    try:
        size = 0
        with stored_path.open("xb") as destination:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_FILE_SIZE:
                    raise HTTPException(status_code=413, detail="PDF exceeds 50 MB")
                destination.write(chunk)

        if summary is None:
            try:
                summary = await summarize_pdf(stored_path)
            except SummarizationError as exc:
                raise HTTPException(status_code=502, detail=str(exc)) from exc

        paper = ResearchPaper(
            title=title,
            author=author,
            file_path=stored_path.relative_to(PROJECT_ROOT).as_posix(),
            summary=summary,
        )
        db.add(paper)
        db.flush()
        response = PaperResponse.model_validate(paper)
        db.commit()
        return response
    except Exception:
        db.rollback()
        stored_path.unlink(missing_ok=True)
        raise
    finally:
        await file.close()


@router.get("api/paper/{paper_id}", response_model=PaperResponse, status_code=200, include_in_schema=False)
async def get_paper(paper_id: int, db: Session = Depends(get_db)) -> PaperResponse:
    paper = db.get(ResearchPaper, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Research paper not found")
    return PaperResponse.model_validate(paper)

@router.get("api/papers", response_model=list[PaperResponse], status_code=200, include_in_schema=False)
async def list_papers(db: Session = Depends(get_db)) -> list[PaperResponse]:
    papers = db.query(ResearchPaper).all()
    return [PaperResponse.model_validate(paper) for paper in papers]