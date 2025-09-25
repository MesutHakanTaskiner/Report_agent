import { useState, useEffect, useCallback } from 'react';
import type { UploadProps } from 'antd';
import type { MessageInstance } from 'antd/es/message/interface';
import type { HookAPI as ModalHookAPI } from 'antd/es/modal/useModal';

import type { FileAttachment, Message, Session } from '../types';
import api from '../../../services/api';

interface UseReportChatDeps {
  messageApi: MessageInstance;
  modalApi: ModalHookAPI;
}

export const useReportChat = ({ messageApi, modalApi }: UseReportChatDeps) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState<FileAttachment[]>([]);
  const [showUploadZone, setShowUploadZone] = useState(true);
  const [selectedModel, setSelectedModel] = useState('GPT-4o');
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string>('default');
  const [collapsed, setCollapsed] = useState(false);
  const [helpDrawerVisible, setHelpDrawerVisible] = useState(false);
  const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentAnalysisType, setCurrentAnalysisType] = useState<string>('summarize');
  const [showWelcomeMessage, setShowWelcomeMessage] = useState(true);

  // Fetch sessions on component mount
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        setIsLoading(true);
        const fetchedSessions = await api.getSessions();
        setSessions(fetchedSessions);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching sessions:', error);
        messageApi.error('Failed to load sessions');
        setIsLoading(false);
      }
    };

    fetchSessions();
  }, [messageApi]);

  // Fetch messages for current session
  useEffect(() => {
    const fetchMessages = async () => {
      if (currentSessionId === 'default') {
        setMessages([]);
        setShowWelcomeMessage(true); // Show welcome message for default session
        return;
      }

      try {
        setIsLoading(true);
        const fetchedMessages = await api.getMessages(currentSessionId);
        setMessages(fetchedMessages);
        
        // Show welcome message only if the session has no messages
        setShowWelcomeMessage(fetchedMessages.length === 0);
        
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching messages:', error);
        messageApi.error('Failed to load messages');
        setIsLoading(false);
      }
    };

    fetchMessages();
  }, [currentSessionId, messageApi]);

  const handleNewAnalysis = useCallback(async () => {
    try {
      const title = `New Analysis ${new Date().toLocaleString()}`;
      const newSession = await api.createSession(title);
      
      setSessions(prev => [newSession, ...prev]);
      setMessages([]);
      setUploadedFiles([]);
      setInputValue('');
      setShowUploadZone(true);
      setShowWelcomeMessage(true); // Reset welcome message for new session
      setCurrentSessionId(newSession.id);

      messageApi.success('New analysis session created');
    } catch (error) {
      console.error('Error creating new session:', error);
      messageApi.error('Failed to create new session');
    }
  }, [messageApi]);

  const handleSessionClick = useCallback(async (sessionId: string) => {
    try {
      setCurrentSessionId(sessionId);
      const sessionMessages = await api.getMessages(sessionId);
      
      setMessages(sessionMessages);
      
      // Show welcome message only if the session has no messages
      setShowWelcomeMessage(sessionMessages.length === 0);
      
      const session = sessions.find(s => s.id === sessionId);
      if (session?.title) {
        messageApi.info(`Loaded session: ${session.title}`);
      }
      
      setShowUploadZone(false);
    } catch (error) {
      console.error('Error loading session:', error);
      messageApi.error('Failed to load session');
    }
  }, [sessions, messageApi]);

  const handleBackToDashboard = () => {
    messageApi.info('Navigating to dashboard...');
  };

  const handleToggleFavorite = useCallback(async (sessionId: string) => {
    try {
      const updatedSession = await api.toggleFavorite(sessionId);
      setSessions(prev => prev.map(s => (s.id === sessionId ? updatedSession : s)));
      messageApi.success(updatedSession.isFavorite ? 'Added to favorites' : 'Removed from favorites');
    } catch (error) {
      console.error('Error toggling favorite:', error);
      messageApi.error('Failed to update favorite status');
    }
  }, [messageApi]);

  const handleDeleteSession = useCallback((sessionId: string) => {
    modalApi.confirm({
      title: 'Delete Session',
      content: 'Are you sure you want to delete this session?',
      onOk: async () => {
        try {
          await api.deleteSession(sessionId);
          setSessions(prev => prev.filter(s => s.id !== sessionId));
          messageApi.success('Session deleted');
          
          if (currentSessionId === sessionId) {
            setCurrentSessionId('default');
            setMessages([]);
            setShowWelcomeMessage(true); // Show welcome message when returning to default session
          }
        } catch (error) {
          console.error('Error deleting session:', error);
          messageApi.error('Failed to delete session');
        }
      }
    });
  }, [modalApi, messageApi, currentSessionId]);

  const handleRenameSession = useCallback(async (sessionId: string, newTitle: string) => {
    try {
      const updatedSession = await api.updateSession(sessionId, newTitle);
      setSessions(prev => prev.map(s => (s.id === sessionId ? updatedSession : s)));
      setEditingSessionId(null);
      messageApi.success('Session renamed');
    } catch (error) {
      console.error('Error renaming session:', error);
      messageApi.error('Failed to rename session');
    }
  }, [messageApi]);

  const handleSend = useCallback(async () => {
    if (!inputValue.trim() && uploadedFiles.length === 0) return;

    // If we're in the default session, create a new session first
    let sessionId = currentSessionId;
    if (sessionId === 'default') {
      try {
        const newSession = await api.createSession(`New Analysis ${new Date().toLocaleString()}`);
        setSessions(prev => [newSession, ...prev]);
        sessionId = newSession.id;
        setCurrentSessionId(sessionId);
      } catch (error) {
        console.error('Error creating session:', error);
        messageApi.error('Failed to create session');
        return;
      }
    }

    // Create user message locally first for immediate feedback
    const newMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
      attachments: uploadedFiles.length > 0 ? [...uploadedFiles] : undefined,
      status: 'sending'
    };

    setMessages(prev => [...prev, newMessage]);
    setInputValue('');
    setShowWelcomeMessage(false); // Hide welcome message when user sends a message

    if (uploadedFiles.length > 0) {
      setShowUploadZone(false);
    }

    try {
      // In a real implementation, we would upload the actual files here
      // For now, we'll just use the file attachments we already have
      const uploadedAttachments: FileAttachment[] = [...uploadedFiles];

      // Send the message to the API with the analysis type
      const sentMessage = await api.sendMessage(
        sessionId, 
        inputValue, 
        uploadedAttachments.length > 0 ? uploadedAttachments : undefined,
        currentAnalysisType
      );
      
      // Update the message status in the UI
      setMessages(prev => prev.map(msg => 
        msg.id === newMessage.id ? { ...sentMessage, id: newMessage.id } : msg
      ));
      
      setUploadedFiles([]);
      
      // The backend will automatically create and send an assistant response
      // We'll poll for new messages to get the assistant's response
      const checkForNewMessages = async () => {
        try {
          const updatedMessages = await api.getMessages(sessionId);
          setMessages(updatedMessages);
        } catch (error) {
          console.error('Error fetching messages:', error);
        }
      };
      
      // Poll a few times to get the assistant's response
      setTimeout(checkForNewMessages, 1000);
      setTimeout(checkForNewMessages, 3000);
      
    } catch (error) {
      console.error('Error sending message:', error);
      messageApi.error('Failed to send message');
      
      // Update the message to show error status
      setMessages(prev => prev.map(msg => 
        msg.id === newMessage.id ? { ...msg, status: 'error' } : msg
      ));
    }
  }, [inputValue, uploadedFiles, currentSessionId, messageApi, currentAnalysisType]);

  const handleAction = useCallback((action: string) => {
    if (action === 'upload') {
      setShowUploadZone(prev => !prev);
      return;
    }

    const actionMessages: Record<string, string> = {
      summarize: 'Please provide a comprehensive summary of the uploaded reports.',
      trends: 'Analyze and identify key trends in the data.',
      kpis: 'Extract and highlight the key performance indicators.',
      actions: 'Generate actionable recommendations based on the analysis.',
      compare: 'Compare the uploaded reports and highlight differences.'
    };

    const msg = actionMessages[action] || 'Processing your request...';
    setInputValue(msg);
    
    // Store the analysis type for the next message send
    setCurrentAnalysisType(action);
  }, []);

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: true,
    accept: '.xlsx,.xls,.csv,.pdf,.vb',
    showUploadList: false,
    beforeUpload: async file => {
      try {
        // Create a temporary file attachment for UI feedback
        const tempFile: FileAttachment = {
          id: Date.now().toString(),
          name: file.name,
          size: file.size,
          type: file.type,
          uploadProgress: 0,
          status: 'uploading'
        };

        setUploadedFiles(prev => [...prev, tempFile]);

        // Actually upload the file to the backend
        const uploadedFile = await api.uploadFile(file);
        
        // Update the file attachment with the real ID from the backend
        setUploadedFiles(prev =>
          prev.map(f => (f.id === tempFile.id ? { ...uploadedFile, uploadProgress: 100, status: 'uploaded' } : f))
        );
        
        messageApi.success(`${file.name} uploaded successfully`);
      } catch (error) {
        console.error('Error uploading file:', error);
        messageApi.error(`Failed to upload ${file.name}`);
      }

      return false;
    }
  };

  const removeUploadedFile = useCallback((fileId: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId));
  }, []);

  return {
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
    isLoading,
    showWelcomeMessage,
    setInputValue,
    setSelectedModel,
    setCollapsed,
    setHelpDrawerVisible,
    setEditingSessionId,
    setEditingTitle,
    setShowWelcomeMessage,
    handleNewAnalysis,
    handleSessionClick,
    handleBackToDashboard,
    handleToggleFavorite,
    handleDeleteSession,
    handleRenameSession,
    handleSend,
    handleAction,
    uploadProps,
    removeUploadedFile
  };
};
