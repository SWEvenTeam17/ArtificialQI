'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import delteIcon from '/public/images/icon.png';
import runIcon from '/public/images/run.png';

const SessionCard = ({ session, deleteSession }) => {
    const router = useRouter();

    return (
        <div className="d-flex flex-column align-items-center">
            <div className="card text-center rounded-5 shadow-sm p-3 mb-2 w-100" style={{ maxWidth: '400px' }}>
                <div className="card-body">
                    <h4 className="card-title text-primary">{session.title}</h4>
                    <p className="card-text">{session.description}</p>
                </div>
                <div className='row row-cols-2'>
                    <div className='col'>
                        <button
                            className="btn btn-danger shadow-sm w-100 rounded-5"
                            onClick={() => {
                                deleteSession(session.id);
                            }}
                        >
                            <Image alt={"Cancella immagine"} width={32} height={32} src={delteIcon} />
                        </button>
                    </div>
                    <div className='col'>
                        <Link
                            href={`/sessions/${session.id}`}
                            onClick={() => router.push(`/sessions/${session.id}`)}
                            className="btn btn-primary shadow-sm w-100 rounded-5"
                        >
                            <Image alt={"Cancella immagine"} width={32} height={32} src={runIcon} />
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SessionCard;
