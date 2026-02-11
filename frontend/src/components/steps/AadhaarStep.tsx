import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { fetchApi } from '@/lib/api';
import { VerificationStep, StepStatus } from '@/lib/types';
import { Fingerprint, ExternalLink, CheckCircle2 } from 'lucide-react';

interface AadhaarStepProps {
    token: string;
    step: VerificationStep;
    onComplete: () => void;
}

export default function AadhaarStep({ token, step, onComplete }: AadhaarStepProps) {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<'start' | 'waiting' | 'verifying' | 'verified'>('start');

    // Check existing state on mount and step updates
    useEffect(() => {
        // If already completed, just show verified
        if (step.status === StepStatus.COMPLETED) {
            setStatus('verified');
            return;
        }

        // Check URL for return from DigiLocker
        const urlParams = new URLSearchParams(window.location.search);
        const urlClientId = urlParams.get('client_id');

        // Check metadata for stored state
        const metadataStatus = step.metadata?.status;
        const metadataClientId = step.metadata?.client_id;

        if (metadataStatus === 'awaiting_redirect' || metadataClientId || urlClientId) {
            console.log("Detected return from DigiLocker or pending verification", { urlClientId, metadataClientId });
            setStatus('verifying');
            completeVerification(urlClientId || metadataClientId);
        }
    }, [step]);

    const initiateVerification = async () => {
        setIsLoading(true);
        setError(null);
        try {
            // Use current page URL as redirect target
            const redirectUrl = window.location.origin + window.location.pathname;

            const response = await fetchApi<{ url: string }>(`/verify/${token}/aadhaar/initiate`, {
                method: 'POST',
                body: JSON.stringify({ redirect_url: redirectUrl })
            });

            if (response.url) {
                setStatus('waiting');
                // Redirect user to DigiLocker
                window.location.href = response.url;
            } else {
                throw new Error("No redirect URL received");
            }
        } catch (err: any) {
            setError(err.message || 'Failed to initiate DigiLocker');
            setIsLoading(false);
        }
    };

    const completeVerification = async (clientId?: string | null) => {
        setIsLoading(true);
        setError(null);
        try {
            // Pass clientId if we have it from URL but backend might have missed it
            await fetchApi(`/verify/${token}/aadhaar/complete`, {
                method: 'POST',
                body: clientId ? JSON.stringify({ client_id: clientId }) : undefined
            });
            setStatus('verified');
        } catch (err: any) {
            console.error("Verification error:", err);
            // If user just came back without completing, show a specific guidance
            if (err.message?.toLowerCase().includes('not found') || err.message?.toLowerCase().includes('session')) {
                setError('DigiLocker verification not completed. Please try again.');
            } else {
                setError(err.message || 'Verification failed. Please try connecting again.');
            }
            setStatus('start');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="w-full">
            <div className="text-center mb-8">
                <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 ${status === 'verified' ? 'bg-green-500/20' : 'bg-blue-500/20'
                    }`}>
                    {status === 'verified' ? (
                        <CheckCircle2 className="w-8 h-8 text-green-400" />
                    ) : (
                        <Fingerprint className="w-8 h-8 text-blue-400" />
                    )}
                </div>
                <h2 className="text-xl font-semibold text-white mb-2">
                    {status === 'verifying' ? 'Verifying Identity...' :
                        status === 'verified' ? 'Identity Verified' : 'Aadhaar Verification'}
                </h2>
                <p className="text-white/60 text-sm max-w-sm mx-auto">
                    {status === 'verifying'
                        ? 'Please wait while we fetch your verified data from DigiLocker.'
                        : status === 'verified'
                            ? 'Great! Your identity has been successfully verified through DigiLocker.'
                            : 'We use DigiLocker to securely verify your identity. You will be redirected to authorize access.'}
                </p>
            </div>

            {error && (
                <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
                    {error}
                </div>
            )}

            <div className="space-y-4">
                {status === 'start' && (
                    <Button
                        onClick={initiateVerification}
                        className="w-full h-12 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold shadow-lg shadow-indigo-500/20"
                        isLoading={isLoading}
                        icon={<ExternalLink className="w-4 h-4" />}
                    >
                        Connect via DigiLocker
                    </Button>
                )}

                {status === 'verifying' && (
                    <Button
                        disabled
                        className="w-full h-12 bg-blue-500/20 text-blue-400"
                        isLoading={true}
                    >
                        Fetching DigiLocker Data...
                    </Button>
                )}

                {status === 'verified' && (
                    <Button
                        onClick={onComplete}
                        className="w-full h-12 bg-green-500 hover:bg-green-600 text-white font-bold text-lg animate-bounce-subtle"
                    >
                        Continue to PAN Verification
                    </Button>
                )}

                <div className="text-center mt-6">
                    <p className="text-[10px] text-white/20 uppercase tracking-[0.2em] font-medium">
                        Secured by SurePass & DigiLocker
                    </p>
                </div>
            </div>
        </div>
    );
}
