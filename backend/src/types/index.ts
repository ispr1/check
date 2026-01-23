export interface User {
  id: string;
  email: string;
  name: string;
  role: 'hr';
  created_at: Date;
}

export interface Candidate {
  id: string;
  name: string;
  email: string;
  phone: string;
  aadhaar_number: string;
  status: 'pending' | 'in_progress' | 'completed';
  created_at: Date;
}

export interface Verification {
  id: string;
  candidate_id: string;
  type: 'identity' | 'address' | 'education' | 'employment';
  status: 'pending' | 'verified' | 'failed';
  data: any;
  verified_at?: Date;
}

export interface TrustScore {
  id: string;
  candidate_id: string;
  overall_score: number;
  identity_score: number;
  address_score: number;
  education_score: number;
  employment_score: number;
  calculated_at: Date;
}
