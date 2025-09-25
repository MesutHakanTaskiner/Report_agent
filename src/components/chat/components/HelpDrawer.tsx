import React from 'react';
import { Drawer, Space, Typography } from 'antd';

const { Title, Text } = Typography;

interface HelpDrawerProps {
  visible: boolean;
  onClose: () => void;
}

const HelpDrawer: React.FC<HelpDrawerProps> = ({ visible, onClose }) => (
  <Drawer title="Help & FAQ" placement="right" onClose={onClose} open={visible} width={400}>
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <div>
        <Title level={5}>How to use Report Agent?</Title>
        <Text>
          1. Upload your business documents (Excel, CSV, PDF)
          <br />
          2. Select an analysis type or ask questions
          <br />
          3. Review the AI-generated insights
          <br />
          4. Export or save your analysis results
        </Text>
      </div>
      <div>
        <Title level={5}>Supported File Types</Title>
        <Text>
          - Excel files (.xlsx, .xls)
          <br />
          - CSV files (.csv)
          <br />
          - PDF documents (.pdf)
          <br />
          - VB Reports (.vb)
        </Text>
      </div>
      <div>
        <Title level={5}>Quick Actions</Title>
        <Text>
          - <strong>Summarize:</strong> Get executive summaries
          <br />
          - <strong>Trends:</strong> Identify patterns and trends
          <br />
          - <strong>KPIs:</strong> Extract key metrics
          <br />
          - <strong>Action Items:</strong> Get recommendations
          <br />
          - <strong>Compare:</strong> Compare multiple reports
        </Text>
      </div>
    </Space>
  </Drawer>
);

export default HelpDrawer;
