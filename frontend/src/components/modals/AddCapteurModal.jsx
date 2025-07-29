import React, { useState, useEffect } from 'react';
import Modal from './Modal';

const AddCapteurModal = ({ isOpen, onClose, onAdd }) => {
  const [nom, setNom] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setNom('');
      setIsSubmitting(false);
    }
  }, [isOpen]);

  const handleSubmit = async () => {
    if (!nom.trim()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onAdd(nom.trim());
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isSubmitting) {
      handleSubmit();
    }
  };

  const content = (
    <div className="mb-4">
      <label htmlFor="capteur-nom" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
        Nom du capteur
      </label>
      <input
        type="text"
        id="capteur-nom"
        value={nom}
        onChange={(e) => setNom(e.target.value)}
        onKeyPress={handleKeyPress}
        className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        placeholder="Exemple : Nord, Sud-Est, Extérieur..."
        autoFocus
      />
      <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
        Exemple : "Nord", "Sud-Est", "Extérieur", etc.
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
      text: isSubmitting ? 'Ajout en cours...' : 'Ajouter',
      class: 'btn-primary',
      id: 'add-capteur-btn',
      onClick: handleSubmit,
      disabled: isSubmitting || !nom.trim()
    }
  ];

  return (
    <Modal
      title="Ajouter un capteur"
      isOpen={isOpen}
      onClose={onClose}
      actions={actions}
    >
      {content}
    </Modal>
  );
};

export default AddCapteurModal;
