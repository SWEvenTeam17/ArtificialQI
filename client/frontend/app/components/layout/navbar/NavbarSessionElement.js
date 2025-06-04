import Link from "next/link";
import { useRouter } from "next/navigation";
export default function NavbarSessionElement({ session }) {
  const router = useRouter();
  return (
    <Link
      href={`/sessions/${session.id}`}
      onClick={() => {
        router.push(`/sessions/${session.id}`);
      }}
      data-bs-dismiss="offcanvas"
      className="btn w-100 mt-2 btn-light rounded-5 border"
    >
      {session.title}
    </Link>
  );
}
