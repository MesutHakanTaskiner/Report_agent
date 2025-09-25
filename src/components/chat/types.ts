export interface FileAttachment {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadProgress: number;
  status: 'uploading' | 'uploaded' | 'error';
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date | string;
  attachments?: FileAttachment[];
  status: 'sending' | 'sent' | 'error';
  isStreaming?: boolean;
}

export interface Session {
  id: string;
  title: string;
  timestamp: Date | string;
  fileCount: number;
  isFavorite?: boolean;
  messages?: Message[];
}
