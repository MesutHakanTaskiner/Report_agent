import React from 'react';
import { Card, Avatar, Typography, Space } from 'antd';
import { RobotOutlined, UserOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import type { Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';

import type { Message } from '../types';
import FileBadge from './FileBadge';
import { formatMessageText } from '../utils';

const { Text, Paragraph } = Typography;

const markdownComponents: Components = {
  code(codeProps) {
    const { inline, className, children, ...props } = codeProps as {
      inline?: boolean;
      className?: string;
      children: React.ReactNode;
    };

    if (inline) {
      return (
        <code className={className} {...props}>
          {children}
        </code>
      );
    }

    return (
      <pre>
        <code className={className} {...props}>
          {children}
        </code>
      </pre>
    );
  },
  a({ node: _node, children, ...props }) {
    return (
      <a {...props} target="_blank" rel="noopener noreferrer">
        {children}
      </a>
    );
  },
};

interface MessageItemProps {
  message: Message;
}

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user';

  const renderContent = () => {
    if (!isUser) {
      return (
        <div className="message-content">
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
            {message.content}
          </ReactMarkdown>
        </div>
      );
    }

    return (
      <Paragraph className="message-content" style={{ margin: 0 }}>
        {formatMessageText(message.content)}
      </Paragraph>
    );
  };

  return (
    <div style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', marginBottom: 16 }}>
      <Space align="start" style={{ maxWidth: '70%' }}>
        {!isUser && <Avatar icon={<RobotOutlined />} style={{ backgroundColor: '#1890ff' }} />}
        <Card style={{ backgroundColor: isUser ? '#e6f7ff' : '#f0f2f5', border: 'none' }} styles={{ body: { padding: '8px 16px' } }}>
          {renderContent()}
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
