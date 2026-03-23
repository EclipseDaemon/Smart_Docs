export interface User {
  id: number
  email: string
  full_name: string | null
  is_active: boolean
  created_at: string
}

export interface Document {
  id: number
  title: string
  original_filename: string
  file_size: number
  file_type: string
  is_processed: boolean
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
  full_name?: string
}

export interface SearchResult {
  documents: Document[]
  total: number
}