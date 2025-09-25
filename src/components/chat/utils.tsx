import React from 'react';
import { FileExcelOutlined, FilePdfOutlined, FileTextOutlined } from '@ant-design/icons';

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${Math.round((bytes / Math.pow(k, i)) * 100) / 100} ${sizes[i]}`;
};

export const getFileIcon = (fileName: string): React.ReactNode => {
  const ext = fileName.split('.').pop()?.toLowerCase();
  switch (ext) {
    case 'xlsx':
    case 'xls':
    case 'csv':
      return <FileExcelOutlined style={{ fontSize: 20, color: '#52c41a' }} />;
    case 'pdf':
      return <FilePdfOutlined style={{ fontSize: 20, color: '#ff4d4f' }} />;
    default:
      return <FileTextOutlined style={{ fontSize: 20, color: '#1890ff' }} />;
  }
};
