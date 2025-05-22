import Link from "next/link";

export default function NavbarSessionElement({ session }) {
  return (
    <Link
      href={`/sessions/${session.id}`}
      data-bs-dismiss="offcanvas"
      className="btn w-100 mt-2 btn-light rounded-5 border"
    >
      {session.title}
    </Link>
  );
}
