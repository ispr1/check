import { Response } from 'express';
import { query } from '../config/database';
import { AuthRequest } from '../middleware/auth.middleware';

export const getVerifications = async (req: AuthRequest, res: Response) => {
  try {
    const result = await query('SELECT * FROM verifications WHERE candidate_id = $1', [req.params.candidateId]);
    res.json(result.rows);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
};

export const startVerification = async (req: AuthRequest, res: Response) => {
  const { candidate_id, type } = req.body;
  
  try {
    const result = await query(
      'INSERT INTO verifications (candidate_id, type, status, data) VALUES ($1, $2, $3, $4) RETURNING *',
      [candidate_id, type, 'pending', {}]
    );
    res.status(201).json(result.rows[0]);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
};
