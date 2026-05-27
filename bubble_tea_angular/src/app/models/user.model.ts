export interface User {
  uid: string;
  name: string | null;
  email: string | null;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData extends LoginData {
  name: string;
}