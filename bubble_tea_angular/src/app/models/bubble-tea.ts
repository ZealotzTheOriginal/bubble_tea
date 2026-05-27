export interface BubbleTea {
  bubbletea_id: number;
  nombre: string;
  tipo_bubbletea: string;
  descripcion: string;
  categoria_id: number | null;
  disponible_caliente: number;
  es_vegano: number;
  tiene_cafeina: number;
  stock: number;
  activo: number;
  precio_M: number | null;
  precio_L: number | null;
  alergenos: string[];
}

export interface BubbleTeaResponse {
  ok: boolean;
  result: BubbleTea[];
}
