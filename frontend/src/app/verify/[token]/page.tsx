'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { fetchApi } from '@/lib/api';
import { VerificationSession } from '@/lib/types';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import PersonalInfoStep from '@/components/steps/PersonalInfoStep';
import FaceVerificationStep from '@/components/steps/FaceVerificationStep';
import PANStep from '@/components/steps/PANStep';
import AadhaarStep from '@/components/steps/AadhaarStep';
import UANStep from '@/components/steps/UANStep';
import { Shield, CheckCircle2, AlertCircle } from 'lucide-react';

export default function VerifyPage() {
    const params = useParams();
    const token = params.token as string;

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [session, setSession] = useState<VerificationSession | null>(null);
    const [isFinalConsent, setIsFinalConsent] = useState(false);

    useEffect(() => {
        if (!token) return;

        const initSession = async () => {
            try {
                // Initialize session
                const data = await fetchApi<VerificationSession>(`/verify/${token}`, {
                    method: 'GET'
                });
                setSession(data);
            } catch (err: any) {
                setError(err.message || 'Failed to initialize verification session');
            } finally {
                setIsLoading(false);
            }
        };

        initSession();
    }, [token]);

    if (isLoading) {
        return (
            <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (error || !session) {
        return (
            <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center p-4">
                <Card className="max-w-md w-full p-8 text-center border-red-500/20 bg-red-500/5">
                    <div className="w-16 h-16 rounded-full bg-red-500/10 flex items-center justify-center mx-auto mb-4">
                        <AlertCircle className="w-8 h-8 text-red-500" />
                    </div>
                    <h1 className="text-xl font-bold text-white mb-2">Verification Failed</h1>
                    <p className="text-white/60 mb-6">{error || 'Session not found'}</p>
                    <p className="text-sm text-white/40">Please check your link or contact support.</p>
                </Card>
            </div>
        );
    }

    const { candidate } = session;
    const currentStep = session.steps.find(s => s.status === 'PENDING' || s.status === 'FAILED');
    // Consider completed if status is SUBMITTED, SCORED or if frontend thinks it's done
    const isComplete = ['SUBMITTED', 'SCORED', 'COMPLETED'].includes(session.status);

    const handleStepComplete = async () => {
        // Refresh session
        try {
            const data = await fetchApi<VerificationSession>(`/verify/${token}`, {
                method: 'GET'
            });
            setSession(data);
        } catch (err) {
            console.error('Failed to refresh session', err);
        }
    };

    const handleSubmitVerification = async () => {
        setIsLoading(true);
        try {
            await fetchApi(`/verify/${token}/submit`, {
                method: 'POST'
            });
            // Refresh to get new status
            await handleStepComplete();
        } catch (err: any) {
            setError(err.message || 'Submission failed');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#0a0a0f] relative overflow-hidden flex flex-col items-center justify-center p-4">
            {/* Background Effects */}
            <div className="absolute inset-0 diamond-pattern opacity-50 pointer-events-none" />
            <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-500/10 rounded-full blur-[150px] pointer-events-none" />

            <motion.div
                layout
                className="w-full max-w-lg z-10"
            >
                <div className="text-center mb-8">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center mx-auto mb-4 backdrop-blur-sm border border-white/5">
                        <Shield className="w-8 h-8 text-indigo-400" />
                    </div>
                    <h1 className="text-2xl font-bold text-white mb-2">
                        {isComplete ? 'Verification Complete' : `Welcome, ${candidate.full_name}`}
                    </h1>
                    {!isComplete && (
                        <p className="text-white/60 text-sm">
                            Step {(session.steps.findIndex(s => s.status === 'PENDING' || s.status === 'FAILED') + 1) || session.steps.length} of {session.steps.length}
                        </p>
                    )}
                </div>

                <Card className="p-1 overflow-hidden">
                    <div className="bg-[#16161f] rounded-xl p-6 md:p-8">
                        {isComplete ? (
                            <div className="text-center py-8">
                                <div className="w-20 h-20 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                                    <CheckCircle2 className="w-10 h-10 text-green-500" />
                                </div>
                                <h2 className="text-xl font-semibold text-white mb-2">All Done!</h2>
                                <p className="text-white/50 mb-8">
                                    Your verification details have been submitted successfully.
                                </p>
                                <Button className="w-full" disabled>
                                    Close Window
                                </Button>
                            </div>
                        ) : currentStep?.step_type === 'PERSONAL_INFO' ? (
                            <PersonalInfoStep
                                token={token}
                                step={currentStep}
                                onComplete={handleStepComplete}
                            />
                        ) : currentStep?.step_type === 'FACE_LIVENESS' ? (
                            <FaceVerificationStep
                                token={token}
                                step={currentStep}
                                onComplete={handleStepComplete}
                            />
                        ) : currentStep?.step_type === 'PAN' ? (
                            <PANStep
                                token={token}
                                step={currentStep}
                                aadhaarStep={session.steps.find(s => s.step_type === 'AADHAAR')}
                                onComplete={handleStepComplete}
                            />
                        ) : currentStep?.step_type === 'AADHAAR' ? (
                            <AadhaarStep
                                token={token}
                                step={currentStep}
                                onComplete={handleStepComplete}
                            />
                        ) : currentStep?.step_type === 'UAN' ? (
                            <UANStep
                                token={token}
                                step={currentStep}
                                onComplete={handleStepComplete}
                            />
                        ) : !currentStep && !isComplete ? (
                            <div className="text-center py-8">
                                <div className="w-16 h-16 bg-green-500/10 rounded-2xl flex items-center justify-center mx-auto mb-6 rotate-3 border border-green-500/20">
                                    <Shield className="w-8 h-8 text-green-400" />
                                </div>
                                <h2 className="text-xl font-semibold text-white mb-2">Final Step: Submission</h2>
                                <p className="text-white/50 mb-8 max-w-sm mx-auto text-sm">
                                    All your documents have been verified. Please provide your final consent to share this information for background verification.
                                </p>

                                <div className="mb-8 p-4 rounded-xl bg-white/[0.02] border border-white/5 text-left flex gap-3">
                                    <input
                                        type="checkbox"
                                        id="final-consent"
                                        className="mt-1 w-4 h-4 rounded border-white/10 bg-white/5 text-indigo-500 focus:ring-indigo-500/50"
                                        checked={isFinalConsent}
                                        onChange={(e) => setIsFinalConsent(e.target.checked)}
                                    />
                                    <label htmlFor="final-consent" className="text-xs text-white/40 leading-relaxed cursor-pointer select-none hover:text-white/60">
                                        I hereby declare that all the information provided by me is true and correct. I authorize Kovanent Identity and verified partners to use this information for my background verification (BGV) purpose.
                                    </label>
                                </div>

                                <Button
                                    className="w-full h-12 text-md font-bold bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-500/20"
                                    onClick={handleSubmitVerification}
                                    isLoading={isLoading}
                                    disabled={!isFinalConsent}
                                >
                                    Confirm & Submit Verification
                                </Button>
                            </div>
                        ) : (
                            <div className="text-center py-12">
                                <p className="text-white/50">
                                    Step type "{currentStep?.step_type}" not implemented yet.
                                </p>
                            </div>
                        )}
                    </div>
                </Card>

                <p className="text-center text-white/20 text-xs mt-8">
                    Powered by Kovanent Identity
                </p>
            </motion.div>
        </div>
    );
}

// Import steps at the top needs to be added too, but strict replace is hard with imports.
// I will use multi-replace to add the import as well.
