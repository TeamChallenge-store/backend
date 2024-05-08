import { useState } from 'react';
import { CustomButton } from '~shared/ui/CustomButton';
import { Icon } from '~shared/ui/Icon';

import css from './Modal.module.scss';

type ModalProps = {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description: string;
};

const Modal = ({ isOpen, onClose, title, description }: ModalProps) => {
  const [isClosing, setIsClosing] = useState(false);

  const handleCloseModal = () => {
    setIsClosing(true);
  };

  const handleAnimationEnd = () => {
    onClose();
  };

  return (
    isOpen && (
      <div className={css.modalContainer}>
        <div
          className={`${css.modal} ${isClosing ? css.fadeOut : ''}`}
          onAnimationEnd={handleAnimationEnd}
        >
          <Icon
            onClick={handleCloseModal}
            className={css.closeIcon}
            type="close"
          />
          <div className={css.modalContent}>
            <h3 className={css.modalTitle}>{title}</h3>
            <span className={css.modalDescription}>{description}</span>
            <CustomButton to="/" bgColor="green" className={css.errorPopUpBtn}>
              Take me back to the home page
            </CustomButton>
          </div>
        </div>
      </div>
    )
  );
};

export { Modal };
