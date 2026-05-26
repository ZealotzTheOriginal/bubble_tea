from typing import List
from models import BubbleTeaDB

def filter_out_inactive_bubble_teas(db_teas: List[BubbleTeaDB]) -> List[BubbleTeaDB]:
    """Filtra y devuelve solo los Bubble Teas que están activos."""
    return [tea for tea in db_teas if tea.active]