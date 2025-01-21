'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const SessionCard = ({ session }) => {
    const router = useRouter();
    return (<div className="col">
        <Link
            href={`/sessions/${session.id}`}
            onClick={() => router.push(`/sessions/${session.id}`)}
            className="card text-decoration-none text-center"
        >
            <h4 className="card-title p-1">{session.title}</h4>
            <p className="card-text p-1">{session.description}</p>
        </Link>
    </div>);
}
export default SessionCard;