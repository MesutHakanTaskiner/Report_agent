import React from 'react';
import { Layout, Button, Typography, List, Card, Space, Input, Dropdown } from 'antd';
import type { MenuProps } from 'antd';
import {
  PlusOutlined,
  FileOutlined,
  EditOutlined,
  DeleteOutlined,
  MoreOutlined
} from '@ant-design/icons';

import type { Session } from '../types';

const { Sider } = Layout;
const { Title, Text } = Typography;

interface SessionSidebarProps {
  collapsed: boolean;
  sessions: Session[];
  currentSessionId: string;
  editingSessionId: string | null;
  editingTitle: string;
  onNewAnalysis: () => void;
  onSessionClick: (sessionId: string) => void;
  onDeleteSession: (sessionId: string) => void;
  onRenameSession: (sessionId: string, newTitle: string) => void;
  onStartEditingSession: (sessionId: string, currentTitle: string) => void;
  onEditingTitleChange: (value: string) => void;
}

const SessionSidebar: React.FC<SessionSidebarProps> = ({
  collapsed,
  sessions,
  currentSessionId,
  editingSessionId,
  editingTitle,
  onNewAnalysis,
  onSessionClick,
  onDeleteSession,
  onRenameSession,
  onStartEditingSession,
  onEditingTitleChange
}) => {
  const sessionMenuItems = (session: Session): MenuProps['items'] => [
    {
      key: 'rename',
      icon: <EditOutlined />,
      label: 'Rename',
      onClick: () => onStartEditingSession(session.id, session.title)
    },
    {
      key: 'delete',
      icon: <DeleteOutlined />,
      label: 'Delete',
      danger: true,
      onClick: () => onDeleteSession(session.id)
    }
  ];

  return (
    <Sider
      width={280}
      collapsed={collapsed}
      collapsedWidth={0}
      style={{ backgroundColor: '#fff', borderRight: '1px solid #e8e8e8', display: 'flex', flexDirection: 'column', height: '100vh' }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
        <div style={{ padding: '16px 24px', borderBottom: '1px solid #e8e8e8' }}>
          <Button icon={<PlusOutlined />} type="primary" block size="large" onClick={onNewAnalysis}>
            New Analysis
          </Button>
        </div>

        <div style={{ flex: 1, overflow: 'auto', padding: '16px 24px' }}>
          <Title level={5} style={{ marginBottom: 16, color: '#666' }}>
            <FileOutlined style={{ marginRight: 8 }} />
            Recent Analyses
          </Title>
          <List
            dataSource={sessions}
            renderItem={session => (
              <Card
                size="small"
                style={{
                  marginBottom: 8,
                  cursor: 'pointer',
                  backgroundColor: session.id === currentSessionId ? '#e6f7ff' : '#fafafa',
                  border: session.id === currentSessionId ? '1px solid #1890ff' : '1px solid #f0f0f0'
                }}
                styles={{ body: { padding: '8px 12px' } }}
                onClick={() => onSessionClick(session.id)}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ flex: 1 }}>
                    {editingSessionId === session.id ? (
                      <Input
                        value={editingTitle}
                        onChange={e => onEditingTitleChange(e.target.value)}
                        onPressEnter={() => onRenameSession(session.id, editingTitle)}
                        onBlur={() => onRenameSession(session.id, editingTitle)}
                        onClick={e => e.stopPropagation()}
                        autoFocus
                        size="small"
                      />
                    ) : (
                      <>
                        <Space>
                          <Text strong style={{ display: 'block', marginBottom: 4 }}>
                            {session.title}
                          </Text>
                        </Space>
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          {new Date(session.timestamp).toLocaleDateString()}  -  {session.fileCount} files
                        </Text>
                      </>
                    )}
                  </div>
                  <Dropdown menu={{ items: sessionMenuItems(session) }} trigger={['click']} placement="bottomRight">
                    <Button
                      type="text"
                      icon={<MoreOutlined />}
                      size="small"
                      onClick={e => {
                        e.stopPropagation();
                      }}
                    />
                  </Dropdown>
                </div>
              </Card>
            )}
          />
        </div>

      </div>
    </Sider>
  );
};

export default SessionSidebar;
