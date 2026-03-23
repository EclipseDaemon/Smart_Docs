import api from '../api/axios'
import type { Document } from '../types'

export const documentService = {
  async getDocuments(): Promise<Document[]> {
    const response = await api.get<{ documents: Document[], total: number }>('/documents')
    return response.data.documents
  },

  async uploadDocument(file: File): Promise<Document> {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post<Document>('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async deleteDocument(id: number): Promise<void> {
    await api.delete(`/documents/${id}`)
  },

  async searchDocuments(query: string): Promise<Document[]> {
    const response = await api.get<{ documents: Document[], total: number }>(`/search?q=${query}`)
    return response.data.documents
  }
}