import React from 'react';
import { Upload, Button, Tooltip, Input } from 'antd';
import type { UploadProps } from 'antd';
import { PaperClipOutlined, SendOutlined } from '@ant-design/icons';

const { TextArea } = Input;

interface MessageComposerProps {
  inputValue: string;
  onInputChange: (value: string) => void;
  onSend: () => void;
  uploadProps: UploadProps;
  isSendDisabled: boolean;
}

const MessageComposer: React.FC<MessageComposerProps> = ({ inputValue, onInputChange, onSend, uploadProps, isSendDisabled }) => (
  <div
    style={{
      display: 'flex',
      gap: 12,
      marginBottom: 12,
      alignItems: 'center'
    }}
  >
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        flex: 1,
        border: '1px solid #d9d9d9',
        borderRadius: 12,
        backgroundColor: '#fff',
        padding: '4px 8px'
      }}
    >
      <Upload {...uploadProps} style={{ display: 'flex', alignItems: 'center' }}>
        <Tooltip title="Attach files">
          <Button
            type="text"
            icon={<PaperClipOutlined />}
            style={{
              height: 40,
              width: 40,
              minWidth: 40,
              borderRadius: 8,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          />
        </Tooltip>
      </Upload>
      <TextArea
        value={inputValue}
        bordered={false}
        onChange={e => onInputChange(e.target.value)}
        onPressEnter={e => {
          if (!e.shiftKey) {
            e.preventDefault();
            onSend();
          }
        }}
        placeholder="Ask about your reports, upload files, or type your message..."
        autoSize={{ minRows: 1, maxRows: 4 }}
        style={{
          flex: 1,
          resize: 'none',
          padding: '8px 12px',
          fontSize: 14,
          lineHeight: '20px'
        }}
      />
    </div>
    <Button
      type="primary"
      icon={<SendOutlined />}
      onClick={onSend}
      disabled={isSendDisabled}
      style={{
        height: 44,
        borderRadius: 12,
        padding: '0 20px',
        display: 'flex',
        alignItems: 'center',
        gap: 8
      }}
    >
      Send
    </Button>
  </div>
);

export default MessageComposer;
