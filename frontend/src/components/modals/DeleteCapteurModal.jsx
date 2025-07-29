import React, { useState } from 'react';
import Modal from './Modal';

const DeleteCapteurModal = ({ isOpen, onClose, onDelete, capteur }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      await onDelete(capteur.id);
    } finally {
      setIsSubmitting(false);
    }
  };

  const content = (
    <div>
      <p className="mb-4">
        Êtes-vous sûr de vouloir supprimer le capteur "{capteur?.nom}" ?
      </p>
      <p className="text-red-500 dark:text-red-400">
        Cette action est irréversible.
      </p>
    </div>
  );

  const actions = [
    {
      text: 'Annuler',
      class: 'btn-secondary',
      onClick: onClose
    },
    {
      text: isSubmitting ? 'Suppression...' : 'Supprimer',
      class: 'btn-danger',
      id: 'delete-capteur-btn',
      onClick: handleSubmit,
      disabled: isSubmitting
    }
  ];

  return (
    <Modal
      title="Supprimer le capteur"
      isOpen={isOpen}
      onClose={onClose}
      actions={actions}
    >
      {content}
    </Modal>
  );
};

export default DeleteCapteurModal;
