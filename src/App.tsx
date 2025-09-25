import { ConfigProvider, App as AntdApp } from 'antd';
import ReportAgentChat from './components/chat/ReportAgentChat';
import './App.css';

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 8,
        },
      }}
    >
      <AntdApp>
        <ReportAgentChat />
      </AntdApp>
    </ConfigProvider>
  );
}

export default App;
