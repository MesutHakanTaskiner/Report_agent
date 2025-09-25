import React, { useEffect, useRef } from 'react';
import { App as AntdApp, Layout, Card, Alert, Typography } from 'antd';

import QuickActions from './components/QuickActions';
import MessageList from './components/MessageList';
import UploadedFilesList from './components/UploadedFilesList';
import MessageComposer from './components/MessageComposer';
import SessionSidebar from './components/SessionSidebar';
import ChatHeader from './components/ChatHeader';
import { useReportChat } from './hooks/useReportChat';

const { Content } = Layout;
const { Text } = Typography;

const ReportAgentChat: React.FC = () => {
  const { message, modal } = AntdApp.useApp();

  const {
    messages,
    inputValue,
    uploadedFiles,
    showUploadZone,
    showWelcomeMessage,
    sessions,
    currentSessionId,
    collapsed,
    editingSessionId,
    editingTitle,
    setInputValue,
    setCollapsed,
    setEditingSessionId,
    setEditingTitle,
    handleNewAnalysis,
    handleSessionClick,
    handleDeleteSession,
    handleDeleteAllSessions,
    handleRenameSession,
    handleSend,
    handleAction,
    uploadProps,
    removeUploadedFile,
  } = useReportChat({ messageApi: message, modalApi: modal });

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const quickActionsDisabled =
    uploadedFiles.length === 0 && messages.every(msg => !msg.attachments || msg.attachments.length === 0);
  const isSendDisabled = !inputValue.trim() && uploadedFiles.length === 0;

  return (
    <Layout style={{ height: '100vh', backgroundColor: '#f0f2f5' }}>
      <SessionSidebar
        collapsed={collapsed}
        sessions={sessions}
        currentSessionId={currentSessionId}
        editingSessionId={editingSessionId}
        editingTitle={editingTitle}
        onNewAnalysis={handleNewAnalysis}
        onSessionClick={handleSessionClick}
        onDeleteSession={handleDeleteSession}
        onDeleteAllSessions={handleDeleteAllSessions}
        onRenameSession={handleRenameSession}
        onStartEditingSession={(sessionId, currentTitle) => {
          setEditingSessionId(sessionId);
          setEditingTitle(currentTitle);
        }}
        onEditingTitleChange={value => setEditingTitle(value)}
      />

      <Layout style={{ backgroundColor: '#fff' }}>
        <ChatHeader
          collapsed={collapsed}
          onToggleSidebar={() => setCollapsed(prev => !prev)}
        />

        <Content
          style={{
            display: 'flex',
            flexDirection: 'column',
            padding: '24px 24px 0',
            backgroundColor: '#fff',
            height: 'calc(100vh - 64px)',
          }}
        >
          <Text type="secondary" style={{ marginBottom: 16 }}>
            I'm your intelligent reporting assistant! Upload Excel files, VB reports, or any business documents, and I'll
            provide comprehensive analysis, extract key insights, and suggest actionable next steps. Perfect for business
            intelligence and strategic decision-making!
          </Text>

          <QuickActions onAction={handleAction} disabled={quickActionsDisabled} showUploadZone={showUploadZone} />

          <Card
            style={{ flex: 1, marginBottom: 16, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}
            styles={{ body: { flex: 1, overflow: 'auto', padding: 16, backgroundColor: '#fafafa' } }}
          >
            {showWelcomeMessage && messages.length === 0 && (
              <div style={{ 
                padding: '20px', 
                background: '#f0f7ff', 
                borderRadius: '8px', 
                marginBottom: '16px',
                border: '1px solid #d6e8ff'
              }}>
                <Text strong style={{ fontSize: '16px', display: 'block', marginBottom: '8px' }}>
                  Welcome to Report Agent!
                </Text>
                <Text>
                  I'm here to help you analyze your business data. To get started:
                </Text>
                <ul style={{ paddingLeft: '20px', margin: '8px 0' }}>
                  <li>Upload your Excel, CSV, PDF, or VB reports using the upload area below</li>
                  <li>Ask me specific questions about your data</li>
                  <li>Try the quick action buttons for common analysis tasks</li>
                </ul>
                <Text type="secondary" style={{ fontSize: '13px', fontStyle: 'italic' }}>
                  This message will disappear once you send your first message.
                </Text>
              </div>
            )}
            <MessageList
              messages={messages}
              showUploadZone={showUploadZone}
              uploadProps={uploadProps}
              messagesEndRef={messagesEndRef}
            />
          </Card>

          <UploadedFilesList files={uploadedFiles} onRemove={removeUploadedFile} />

          <MessageComposer
            inputValue={inputValue}
            onInputChange={value => setInputValue(value)}
            onSend={handleSend}
            uploadProps={uploadProps}
            isSendDisabled={isSendDisabled}
          />

          <Alert
            message="Reporting Agent can analyze complex data and provide insights. Please verify important business decisions."
            type="info"
            showIcon={false}
            style={{
              marginBottom: 0,
              padding: '8px 16px',
              fontSize: 12,
              borderRadius: 0,
              marginLeft: -24,
              marginRight: -24,
            }}
          />
        </Content>
      </Layout>
    </Layout>
  );
};

export default ReportAgentChat;
