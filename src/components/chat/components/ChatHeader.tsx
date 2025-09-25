import React from 'react';
import { Layout, Space, Typography, Button } from 'antd';
import { RobotOutlined, MenuFoldOutlined, MenuUnfoldOutlined } from '@ant-design/icons';

const { Header } = Layout;
const { Title, Text } = Typography;

interface ChatHeaderProps {
  collapsed: boolean;
  onToggleSidebar: () => void;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ collapsed, onToggleSidebar }) => {

  return (
    <Header
      style={{
        backgroundColor: '#fff',
        padding: '0 24px',
        borderBottom: '1px solid #e8e8e8',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}
    >
      <Space size="large">
        <Button type="text" icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} onClick={onToggleSidebar} style={{ fontSize: 16 }} />
        <Title level={3} style={{ margin: 0, display: 'flex', alignItems: 'center' }}>
          <RobotOutlined style={{ marginRight: 8 }} />
          Reporting Agent
        </Title>
      </Space>
      <div></div> {/* Empty div to maintain space-between layout */}
    </Header>
  );
};

export default ChatHeader;
