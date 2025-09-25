import React from 'react';
import type { RefObject } from 'react';
import { Upload } from 'antd';
import type { UploadProps } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

import type { Message } from '../types';
import MessageItem from './MessageItem';

const { Dragger } = Upload;

interface MessageListProps {
  messages: Message[];
  showUploadZone: boolean;
  uploadProps: UploadProps;
  messagesEndRef: RefObject<HTMLDivElement | null>;
}

const MessageList: React.FC<MessageListProps> = ({ messages, showUploadZone, uploadProps, messagesEndRef }) => (
  <div style={{ minHeight: 200 }}>
    {messages.map(msg => (
      <MessageItem key={msg.id} message={msg} />
    ))}

    {showUploadZone && messages.length === 0 && (
      <div style={{ marginTop: 16, marginBottom: 16 }}>
        <Dragger {...uploadProps} style={{ backgroundColor: '#fff' }}>
          <p className="ant-upload-drag-icon">
            <UploadOutlined style={{ fontSize: 48, color: '#1890ff' }} />
          </p>
          <p className="ant-upload-text">Drop your reports here for analysis</p>
          <p className="ant-upload-hint">Supports Excel, CSV, PDF, and VB report files</p>
        </Dragger>
      </div>
    )}

    <div ref={messagesEndRef} />
  </div>
);

export default MessageList;
