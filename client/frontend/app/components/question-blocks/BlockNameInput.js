export function BlockNameInput({ inputRefs }) {
  return (
    <div className="row text-center justify-content-center m-3 ">
      <div className="col-12 col-md-6">
        <div className="form-floating">
          <input
            ref={(el) => (inputRefs.current["block_name"] = el)}
            id="block_name"
            name="block_name"
            className="form-control rounded-5"
            placeholder="Nome insieme"
          />
          <label htmlFor="block_name">Nome dell&apos;insieme di domande</label>
        </div>
      </div>
    </div>
  );
}
