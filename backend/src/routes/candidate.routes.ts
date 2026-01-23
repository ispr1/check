import { Router } from 'express';
import { authenticate, authorizeHR } from '../middleware/auth.middleware';
import { getCandidates, getCandidate, createCandidate } from '../controllers/candidate.controller';

const router = Router();

router.use(authenticate, authorizeHR);

router.get('/', getCandidates);
router.get('/:id', getCandidate);
router.post('/', createCandidate);

export default router;
