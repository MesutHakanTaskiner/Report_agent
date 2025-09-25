import React from 'react';
import { Space } from 'antd';

import type { FileAttachment } from '../types';
import FileBadge from './FileBadge';

interface UploadedFilesListProps {
  files: FileAttachment[];
  onRemove: (id: string) => void;
}

const UploadedFilesList: React.FC<UploadedFilesListProps> = ({ files, onRemove }) => {
  if (files.length === 0) {
    return null;
  }

  return (
    <div style={{ marginBottom: 8 }}>
      <Space wrap>
        {files.map(file => (
          <FileBadge key={file.id} file={file} onRemove={() => onRemove(file.id)} />
        ))}
      </Space>
    </div>
  );
};

export default UploadedFilesList;
