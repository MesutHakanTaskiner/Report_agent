import type { Message } from './types';

export const mockSessionMessages: Record<string, Message[]> = {
  '1': [
    {
      id: 'm1',
      role: 'assistant',
      content: "I've analyzed your Q3 sales reports. Here are the key findings:",
      timestamp: new Date(Date.now() - 86400000),
      status: 'sent'
    },
    {
      id: 'm2',
      role: 'user',
      content: 'What are the main trends in revenue?',
      timestamp: new Date(Date.now() - 86300000),
      status: 'sent'
    },
    {
      id: 'm3',
      role: 'assistant',
      content: 'Revenue increased by 23% compared to Q2, with strongest growth in the enterprise segment (+45%). Digital products showed exceptional performance.',
      timestamp: new Date(Date.now() - 86200000),
      status: 'sent'
    }
  ],
  '2': [
    {
      id: 'm4',
      role: 'assistant',
      content: 'Marketing report analysis complete. Campaign performance shows mixed results.',
      timestamp: new Date(Date.now() - 172800000),
      status: 'sent'
    },
    {
      id: 'm5',
      role: 'user',
      content: 'Which campaigns performed best?',
      timestamp: new Date(Date.now() - 172700000),
      status: 'sent'
    },
    {
      id: 'm6',
      role: 'assistant',
      content: 'Social media campaigns had 3x ROI, while email marketing achieved 45% open rates. Paid search needs optimization.',
      timestamp: new Date(Date.now() - 172600000),
      status: 'sent'
    }
  ],
  '3': [
    {
      id: 'm7',
      role: 'assistant',
      content: 'Financial dashboard loaded. All KPIs are within expected ranges.',
      timestamp: new Date(Date.now() - 259200000),
      status: 'sent'
    },
    {
      id: 'm8',
      role: 'user',
      content: 'Show me the cash flow analysis',
      timestamp: new Date(Date.now() - 259100000),
      status: 'sent'
    },
    {
      id: 'm9',
      role: 'assistant',
      content: 'Cash flow remains positive with $2.3M in operating activities. Working capital improved by 15%.',
      timestamp: new Date(Date.now() - 259000000),
      status: 'sent'
    }
  ]
};

