'use client'; // This directive marks this component as a Client Component.


export default function Page() {
    async function onSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = {
            title: formData.get('title'),
            description: formData.get('description')
        };

        const response = await fetch('http://localhost:8000/session_list/', {
            method: 'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data),
        });

        if(response.ok)
        {
            event.target.reset();
        }
    }

    return (
        <div className="container align-items-center">
            <div className="card rounded-5 text-center">
                <div className="card-header">Crea una nuova sessione</div>
                <div className="card-body">
                    Inserisci i dati richiesti qui sotto
                    <div className="mt-3">
                        <form onSubmit={onSubmit}>
                            <div className="form-floating mb-3">
                                <input type="text" className="form-control rounded-5" id="title" name="title" placeholder="Titolo" />
                                <label htmlFor="title">Titolo</label>
                            </div>
                            <div className="form-floating mb-3">
                                <input type="text" className="form-control rounded-5" id="description" name="description" placeholder="Descrizione" />
                                <label htmlFor="description">Descrizione</label>
                            </div>
                            <div className="text-center align-items-center col-12">
                                <button type="submit" className="btn btn-primary w-50 rounded-5">Crea</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}
