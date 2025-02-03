'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import delteIcon from '/public/images/icon.png';

const SessionCard = ({ session, deleteSession }) => {
    const router = useRouter();

    return (
            <div className="card text-center rounded-5 shadow hover-grow p-3 mb-2 w-100" style={{ maxWidth: '400px' }}>
                <Link
                    href={`/sessions/${session.id}`}
                    onClick={() => router.push(`/sessions/${session.id}`)}
                    className="text-decoration-none text-dark"
                >
                    <div className="card-body">
                        <h4 className="card-title text-primary">{session.title}</h4>
                        <p className="card-text">{session.description}</p>
                    </div>
                </Link>
                <div className='row justify-content-center'>
                    <div className='col'>
                        <button
                            className="btn btn-danger shadow-sm w-100 rounded-5"
                            onClick={() => {
                                deleteSession(session.id);
                            }}
                        >
                            <Image alt={"Cancella sessione"} width={32} height={32} src={delteIcon} />
                        </button>
                    </div>
                </div>
            </div>
    );
};

export default SessionCard;
