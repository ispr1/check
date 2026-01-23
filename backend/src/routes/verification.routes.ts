import { Router } from 'express';
import { authenticate, authorizeHR } from '../middleware/auth.middleware';
import { getVerifications, startVerification } from '../controllers/verification.controller';

const router = Router();

router.use(authenticate, authorizeHR);

router.get('/candidate/:candidateId', getVerifications);
router.post('/start', startVerification);

export default router;
