import { Response } from 'express';
import { query } from '../config/database';
import { AuthRequest } from '../middleware/auth.middleware';

export const getCandidates = async (req: AuthRequest, res: Response) => {
  try {
    const result = await query('SELECT * FROM candidates ORDER BY created_at DESC');
    res.json(result.rows);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
};

export const getCandidate = async (req: AuthRequest, res: Response) => {
  try {
    const result = await query('SELECT * FROM candidates WHERE id = $1', [req.params.id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Candidate not found' });
    }
    res.json(result.rows[0]);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
};

export const createCandidate = async (req: AuthRequest, res: Response) => {
  const { name, email, phone, aadhaar_number } = req.body;
  
  try {
    const result = await query(
      'INSERT INTO candidates (name, email, phone, aadhaar_number, status) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [name, email, phone, aadhaar_number, 'pending']
    );
    res.status(201).json(result.rows[0]);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
};
