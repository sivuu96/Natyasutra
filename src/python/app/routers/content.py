from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/items")
def list_items(limit: int = 50, db: Session = Depends(get_db)) -> list[dict]:
    """Published, public items from cnt_item. Only the card fields are returned."""
    limit = max(1, min(limit, 100))
    rows = db.execute(
        text(
            """
            SELECT id, kind, slug, title, short_description
            FROM cnt_item
            WHERE status = 'published'
              AND visibility = 'public'
              AND deleted_at IS NULL
            ORDER BY id
            LIMIT :limit
            """
        ),
        {"limit": limit},
    ).mappings()
    return [dict(row) for row in rows]
