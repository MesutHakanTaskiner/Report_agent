import React from 'react';
import { Button, Space } from 'antd';
import {
  UploadOutlined,
  FileSearchOutlined,
  LineChartOutlined,
  BarChartOutlined
} from '@ant-design/icons';

interface QuickActionsProps {
  onAction: (action: string) => void;
  disabled: boolean;
  showUploadZone: boolean;
}

const QuickActions: React.FC<QuickActionsProps> = ({ onAction, disabled, showUploadZone }) => {
  const actions = [
    { key: 'upload', label: showUploadZone ? 'Hide Upload' : 'Upload Report', icon: <UploadOutlined /> },
    { key: 'summarize', label: 'Summarize', icon: <FileSearchOutlined /> },
    { key: 'trends', label: 'Analyze Trends', icon: <LineChartOutlined /> },
    { key: 'kpis', label: 'Extract KPIs', icon: <BarChartOutlined /> }
  ];

  return (
    <Space wrap style={{ marginBottom: 16 }}>
      {actions.map(action => (
        <Button
          key={action.key}
          icon={action.icon}
          onClick={() => onAction(action.key)}
          disabled={disabled && action.key !== 'upload'}
          type={action.key === 'upload' ? 'primary' : 'default'}
        >
          {action.label}
        </Button>
      ))}
    </Space>
  );
};

export default QuickActions;
