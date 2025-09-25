import React, { useEffect, useRef } from 'react';
import { App as AntdApp, Layout, Card, Alert, Typography } from 'antd';

import QuickActions from './components/QuickActions';
import MessageList from './components/MessageList';
import UploadedFilesList from './components/UploadedFilesList';
import MessageComposer from './components/MessageComposer';
import SessionSidebar from './components/SessionSidebar';
import ChatHeader from './components/ChatHeader';
import HelpDrawer from './components/HelpDrawer';
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
    selectedModel,
    sessions,
    currentSessionId,
    collapsed,
    helpDrawerVisible,
    editingSessionId,
    editingTitle,
    setInputValue,
    setSelectedModel,
    setCollapsed,
    setHelpDrawerVisible,
    setEditingSessionId,
    setEditingTitle,
    handleNewAnalysis,
    handleSessionClick,
    handleBackToDashboard,
    handleToggleFavorite,
    handleDeleteSession,
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
        onBackToDashboard={handleBackToDashboard}
        onNewAnalysis={handleNewAnalysis}
        onSessionClick={handleSessionClick}
        onToggleFavorite={handleToggleFavorite}
        onDeleteSession={handleDeleteSession}
        onRenameSession={handleRenameSession}
        onStartEditingSession={(sessionId, currentTitle) => {
          setEditingSessionId(sessionId);
          setEditingTitle(currentTitle);
        }}
        onEditingTitleChange={value => setEditingTitle(value)}
        onHelpClick={() => setHelpDrawerVisible(true)}
      />

      <Layout style={{ backgroundColor: '#fff' }}>
        <ChatHeader
          collapsed={collapsed}
          onToggleSidebar={() => setCollapsed(prev => !prev)}
          selectedModel={selectedModel}
          onModelChange={setSelectedModel}
          messageApi={message}
          modalApi={modal}
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

      <HelpDrawer visible={helpDrawerVisible} onClose={() => setHelpDrawerVisible(false)} />
    </Layout>
  );
};

export default ReportAgentChat;



