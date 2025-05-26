import Image from "next/image";
import cancelIcon from "/public/images/cancel.png";
import deleteIcon from "/public/images/icon.png";
import doneIcon from "/public/images/done.png";
import editIcon from "/public/images/edit.png";
import { useSessionCard } from "@/app/components/contexts/session/SessionCardContext";

export default function SessionCardActions() {
  const { isEditing, startEditing, cancelEditing, saveChanges, removeSession } =
    useSessionCard();

  return (
    <div className="row justify-content-center">
      {isEditing ? (
        <>
          <div className="col">
            <button
              data-cy="cancel-button"
              className="btn btn-danger shadow-sm w-100 rounded-5"
              onClick={cancelEditing}
            >
              <Image alt="Annulla" width={32} height={32} src={cancelIcon} />
            </button>
          </div>
          <div className="col">
            <button
              data-cy="save-button"
              className="btn btn-success shadow-sm w-100 rounded-5"
              onClick={saveChanges}
            >
              <Image alt="Salva" width={32} height={32} src={doneIcon} />
            </button>
          </div>
        </>
      ) : (
        <>
          <div className="col">
            <button
              data-cy="delete-button"
              className="btn btn-danger shadow-sm w-100 rounded-5"
              onClick={removeSession}
            >
              <Image
                alt="Cancella sessione"
                width={32}
                height={32}
                src={deleteIcon}
              />
            </button>
          </div>
          <div className="col">
            <button
              data-cy="edit-button"
              className="btn btn-primary shadow-sm w-100 rounded-5"
              onClick={startEditing}
            >
              <Image
                alt="Modifica sessione"
                width={32}
                height={32}
                src={editIcon}
              />
            </button>
          </div>
        </>
      )}
    </div>
  );
}
