import React from 'react';
import { Layout, Space, Typography, Button, Select, Avatar, Dropdown } from 'antd';
import type { MenuProps } from 'antd';
import type { MessageInstance } from 'antd/es/message/interface';
import type { HookAPI as ModalHookAPI } from 'antd/es/modal/useModal';
import {
  RobotOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UserOutlined,
  DownOutlined,
  SettingOutlined,
  LogoutOutlined,
  ProfileOutlined
} from '@ant-design/icons';

const { Header } = Layout;
const { Title, Text } = Typography;

interface ChatHeaderProps {
  collapsed: boolean;
  onToggleSidebar: () => void;
  selectedModel: string;
  onModelChange: (value: string) => void;
  messageApi: MessageInstance;
  modalApi: ModalHookAPI;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ collapsed, onToggleSidebar, selectedModel, onModelChange, messageApi, modalApi }) => {
  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <ProfileOutlined />,
      label: 'Profile',
      onClick: () => messageApi.info('Opening profile...')
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      onClick: () => messageApi.info('Opening settings...')
    },
    { type: 'divider' },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Sign Out',
      onClick: () => {
        modalApi.confirm({
          title: 'Sign Out',
          content: 'Are you sure you want to sign out?',
          onOk: () => messageApi.success('Signed out successfully')
        });
      }
    }
  ];

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
        <Select
          value={selectedModel}
          onChange={onModelChange}
          style={{ width: 120 }}
          options={[
            { value: 'GPT-4o', label: 'GPT-4o' },
            { value: 'GPT-4', label: 'GPT-4' },
            { value: 'GPT-3.5', label: 'GPT-3.5' }
          ]}
        />
      </Space>

      <Dropdown menu={{ items: userMenuItems }} trigger={['click']}>
        <Button type="text" style={{ padding: '4px 12px', height: 'auto' }}>
          <Space size={8}>
            <Avatar style={{ backgroundColor: '#1890ff' }} icon={<UserOutlined />} />
            <div style={{ textAlign: 'left' }}>
              <Text strong style={{ display: 'block', fontSize: 14 }}>
                Super
              </Text>
              <Text type="secondary" style={{ fontSize: 12 }}>
                Super Admin
              </Text>
            </div>
            <DownOutlined style={{ fontSize: 12 }} />
          </Space>
        </Button>
      </Dropdown>
    </Header>
  );
};

export default ChatHeader;
