import React from 'react';
import { Card, Avatar, Typography, Space } from 'antd';
import { RobotOutlined, UserOutlined } from '@ant-design/icons';

import type { Message } from '../types';
import FileBadge from './FileBadge';
import { formatMessageText } from '../utils';

const { Text, Paragraph } = Typography;

interface MessageItemProps {
  message: Message;
}

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', marginBottom: 16 }}>
      <Space align="start" style={{ maxWidth: '70%' }}>
        {!isUser && <Avatar icon={<RobotOutlined />} style={{ backgroundColor: '#1890ff' }} />}
        <Card style={{ backgroundColor: isUser ? '#e6f7ff' : '#f0f2f5', border: 'none' }} styles={{ body: { padding: '8px 16px' } }}>
          <Paragraph className="message-content" style={{ margin: 0 }}>
            {formatMessageText(message.content)}
          </Paragraph>
          {message.isStreaming && (
            <span className="typing-indicator" style={{ marginLeft: 4 }}>
              <span>.</span>
              <span>.</span>
              <span>.</span>
            </span>
          )}
          {message.attachments && message.attachments.length > 0 && (
            <div style={{ marginTop: 8 }}>
              {message.attachments.map(file => (
                <FileBadge key={file.id} file={file} />
              ))}
            </div>
          )}
          <div style={{ marginTop: 4 }}>
            <Text type="secondary" style={{ fontSize: 12 }}>
              {new Date(message.timestamp).toLocaleTimeString()}
            </Text>
          </div>
        </Card>
        {isUser && <Avatar icon={<UserOutlined />} style={{ backgroundColor: '#87d068' }} />}
      </Space>
    </div>
  );
};

export default MessageItem;
