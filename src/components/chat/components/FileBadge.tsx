import React from 'react';
import { Tag, Space, Typography, Progress } from 'antd';

import type { FileAttachment } from '../types';
import { formatFileSize, getFileIcon } from '../utils';

const { Text } = Typography;

interface FileBadgeProps {
  file: FileAttachment;
  onRemove?: () => void;
}

const FileBadge: React.FC<FileBadgeProps> = ({ file, onRemove }) => (
  <Tag style={{ padding: '4px 8px', marginRight: 8, marginBottom: 8 }} closable={!!onRemove} onClose={onRemove}>
    <Space size={4}>
      {getFileIcon(file.name)}
      <span>{file.name}</span>
      <Text type="secondary" style={{ fontSize: 12 }}>
        ({formatFileSize(file.size)})
      </Text>
    </Space>
    {file.status === 'uploading' && (
      <Progress percent={file.uploadProgress} size="small" showInfo={false} style={{ width: 60, marginLeft: 8 }} />
    )}
  </Tag>
);

export default FileBadge;
