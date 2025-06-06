import Image from "next/image";
import cancelIcon from "/public/images/cancel.png";
import delteIcon from "/public/images/icon.png";
import doneIcon from "/public/images/done.png";
import editIcon from "/public/images/edit.png";
import { useSessionCard } from "@/app/components/contexts/session/SessionCardContext";

export default function SessionCardActions() {
  const { isEditing, startEditing, cancelEditing, saveChanges, removeSession } =
    useSessionCard();

  return (
    <div className="row justify-content-center">
      <div className="col">
        <button
          className="btn btn-danger shadow-sm w-100 rounded-5"
          onClick={isEditing ? cancelEditing : removeSession}
        >
          <Image
            alt={isEditing ? "Annulla" : "Cancella sessione"}
            width={32}
            height={32}
            src={isEditing ? cancelIcon : delteIcon}
          />
        </button>
      </div>
      <div className="col">
        <button
          className={`btn ${isEditing ? "btn-success" : "btn-primary"} shadow-sm w-100 rounded-5`}
          onClick={isEditing ? saveChanges : startEditing}
        >
          <Image
            alt={isEditing ? "Salva" : "Modifica sessione"}
            width={32}
            height={32}
            src={isEditing ? doneIcon : editIcon}
          />
        </button>
      </div>
    </div>
  );
}
