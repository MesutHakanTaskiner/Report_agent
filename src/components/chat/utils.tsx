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

/**
 * Format message text to preserve line breaks and spacing
 * This is a simple approach that doesn't require additional libraries
 */
export const formatMessageText = (text: string): React.ReactNode => {
  if (!text) return null;
  
  // Split by line breaks and create an array of elements
  const lines = text.split('\n');
  
  return (
    <>
      {lines.map((line, i) => (
        <React.Fragment key={i}>
          {line}
          {i < lines.length - 1 && <br />}
        </React.Fragment>
      ))}
    </>
  );
};
