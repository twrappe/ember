export interface DailyMetric {
  date: string;
  hrv: number;
  sleep: number;       // hours
  readiness: number;   // 0-100
  riskScore: number;   // 0-100, mania onset risk
}

export interface Alert {
  id: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high';
  message: string;
  metric: string;
  value: number;
  threshold: number;
  dismissed: boolean;
}

export interface EmberState {
  metrics: DailyMetric[];
  alerts: Alert[];
  currentRisk: number;
  lastSync: string;
}
