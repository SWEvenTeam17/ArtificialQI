'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const SessionCard = ({ session, deleteSession }) => {
    const router = useRouter();

    return (
        <div className="d-flex flex-column align-items-center">
            <div className="card text-center shadow-sm p-3 mb-2 w-100" style={{ maxWidth: '400px' }}>
                <Link
                    href={`/sessions/${session.id}`}
                    onClick={() => router.push(`/sessions/${session.id}`)}
                    className="text-decoration-none text-dark"
                >
                    <div className="card-body">
                        <h4 className="card-title">{session.title}</h4>
                        <p className="card-text">{session.description}</p>
                    </div>
                </Link>
            </div>
            <button
                className="btn btn-danger w-100"
                onClick={() => {
                    deleteSession(session.id);
                }}
            >
                Delete Session
            </button>
        </div>
    );
};

export default SessionCard;
