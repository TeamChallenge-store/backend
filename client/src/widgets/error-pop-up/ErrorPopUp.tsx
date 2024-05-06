import { useState } from 'react';
import { Modal } from '~shared/ui//Modal';

const ErrorPopUp = () => {
  const [isModalOpen, setIsModalOpen] = useState(true);

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <Modal
      isOpen={isModalOpen}
      onClose={closeModal}
      title="Something went wrong."
      description="There was a failure. Please try again."
    />
  );
};

export { ErrorPopUp };
