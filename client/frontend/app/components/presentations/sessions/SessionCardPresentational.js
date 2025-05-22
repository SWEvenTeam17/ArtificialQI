import delteIcon from "/public/images/icon.png";
import editIcon from "/public/images/edit.png";
import doneIcon from "/public/images/done.png";
import cancelIcon from "/public/images/cancel.png";
import Image from "next/image";
import Link from "next/link";

export default function SessionCardPresentational({
  isEditing,
  session,
  editedTitle,
  editedDescription,
  setIsEditing,
  setEditedTitle,
  setEditedDescription,
  handleSave,
}) {
  return (
    <div className="card text-center rounded-5 border-light shadow hover-grow p-3 mb-2 w-100">
      <div className="card-body">
        {isEditing ? (
          <>
            <input
              type="text"
              className="form-control rounded-5 mb-2"
              placeholder="Nome"
              value={editedTitle}
              onChange={(e) => setEditedTitle(e.target.value)}
            />
            <input
              type="text"
              className="form-control rounded-5"
              placeholder="Descrizione"
              value={editedDescription}
              onChange={(e) => setEditedDescription(e.target.value)}
            />
          </>
        ) : (
          <Link
            href={`/sessions/${session.id}`}
            className="text-decoration-none text-dark"
          >
            <h4 className="card-title text-primary">{session.title}</h4>
            <p className="card-text">{session.description}</p>
          </Link>
        )}
      </div>
      <div className="row justify-content-center">
        <div className="col">
          {isEditing ? (
            <button
              className="btn btn-danger shadow-sm w-100 rounded-5"
              onClick={() => {
                setIsEditing(false);
                setEditedTitle(session.title);
                setEditedDescription(session.description);
              }}
            >
              <Image alt={"Annulla"} width={32} height={32} src={cancelIcon} />
            </button>
          ) : (
            <button
              className="btn btn-danger shadow-sm w-100 rounded-5"
              onClick={() => {
                deleteSession(session.id);
              }}
            >
              <Image
                alt={"Cancella sessione"}
                width={32}
                height={32}
                src={delteIcon}
              />
            </button>
          )}
        </div>
        <div className="col">
          {isEditing ? (
            <button
              className="btn btn-success shadow-sm w-100 rounded-5"
              onClick={handleSave}
            >
              <Image alt={"Salva"} width={32} height={32} src={doneIcon} />
            </button>
          ) : (
            <button
              className="btn btn-primary shadow-sm w-100 rounded-5"
              onClick={() => setIsEditing(true)}
            >
              <Image
                alt={"Modifica sessione"}
                width={32}
                height={32}
                src={editIcon}
              />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
