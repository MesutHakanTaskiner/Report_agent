import axios from 'axios';
import type { FileAttachment, Message, Session } from '../components/chat/types';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Sessions API
export const getSessions = async (): Promise<Session[]> => {
  const response = await api.get('/sessions');
  return response.data;
};

export const getSession = async (sessionId: string): Promise<Session> => {
  const response = await api.get(`/sessions/${sessionId}`);
  return response.data;
};

export const createSession = async (title: string): Promise<Session> => {
  const response = await api.post('/sessions', { title });
  return response.data;
};

export const updateSession = async (sessionId: string, title: string): Promise<Session> => {
  const response = await api.put(`/sessions/${sessionId}`, { title });
  return response.data;
};

export const deleteSession = async (sessionId: string): Promise<void> => {
  await api.delete(`/sessions/${sessionId}`);
};

export const toggleFavorite = async (sessionId: string): Promise<Session> => {
  const response = await api.put(`/sessions/${sessionId}/favorite`);
  return response.data;
};

// Messages API
export const getMessages = async (sessionId: string): Promise<Message[]> => {
  const response = await api.get(`/messages/${sessionId}`);
  return response.data;
};

export const sendMessage = async (
  sessionId: string, 
  content: string, 
  attachments?: FileAttachment[], 
  analysisType?: string
): Promise<Message> => {
  const response = await api.post(`/messages/${sessionId}`, {
    content,
    role: 'user',
    attachments,
    analysis_type: analysisType || 'summarize',
  });
  return response.data;
};

// Files API
export const uploadFile = async (file: File): Promise<FileAttachment> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_URL}/files/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const deleteFile = async (fileId: string): Promise<void> => {
  await api.delete(`/files/${fileId}`);
};

export default {
  getSessions,
  getSession,
  createSession,
  updateSession,
  deleteSession,
  toggleFavorite,
  getMessages,
  sendMessage,
  uploadFile,
  deleteFile,
};
