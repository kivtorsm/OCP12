USE epic_events;

INSERT INTO department (`name`)
VALUES
    ('Gestion'),
    ('Commercial'),
    ('Support');

INSERT INTO permission (`object_type`, `crud_action`, `object_list`, `object_field`)
VALUES
    ('employee', 'create', 'na', 'na'),
    ('employee', 'update', 'all', 'all'),
    ('employee', 'delete', 'all', 'na'),
    ('contract', 'create', 'na', 'na'),
    ('contract', 'update', 'all', 'all'),
    ('event', 'update', 'all', 'support_contact_id'),
    ('client', 'create', 'na', 'na'),
    ('client', 'update', 'all', 'all'),
    ('contract', 'update', 'owned', 'all'),
    ('event', 'create', 'all', 'all'),
    ('event', 'update', 'owned', 'all'),
    ('event', 'filter_no_support', 'no_support', 'na'),
    ('contract', 'filter_no_signature', 'no_signature', 'na'),
    ('contract', 'filter_due_amount', 'due_amount', 'na'),
    ('event', 'filter_owned', 'owned', 'na');

INSERT INTO department_permission (`department_id`, `permission_id`)
VALUES
    ('1', '1'),
    ('1', '2'),
    ('1', '3'),
    ('1', '4'),
    ('1', '5'),
    ('1', '6'),
    ('2', '7'),
    ('2', '8'),
    ('2', '9'),
    ('2', '10'),
    ('3', '11'),
    ('1', '12'),
    ('2', '13'),
    ('2', '14'),
    ('3', '15');

INSERT INTO employee (`first_name`, `last_name`, `email`, `department_id`, `encoded_hash`)
VALUES
    ('albert', 'camus', 'gestion1', 1, '$argon2id$v=19$m=65536,t=3,p=4$YnFFKptVhaYFqldkb7rETw$lFei5iQFlrNwFv11Jf/HSAXwZ16THNo5l2Q2JNcY/ck'),
    ('victor', 'hugo', 'commercial1', 2, '$argon2id$v=19$m=65536,t=3,p=4$/kUTgWrAhFPVdC267akARQ$mwSpL0ue2y6A/83w7DCW4392Mb4wNdLo/3oewooObRA'),
    ('jean-baptiste', 'poquelin', 'support1', 3, '$argon2id$v=19$m=65536,t=3,p=4$8UjK8e2GJL2hC7yRi0GRNg$XtdtCN3GNDUPH3YWBAyqyEXXOvQJfXvCcAmOVOEd3Ww'),
    ('gestion ', '2', 'gestion2', 1, '$argon2id$v=19$m=65536,t=3,p=4$8UjK8e2GJL2hC7yRi0GRNg$XtdtCN3GNDUPH3YWBAyqyEXXOvQJfXvCcAmOVOEd3Ww'),
    ('commercial', '2', 'commercial2', 2, '$argon2id$v=19$m=65536,t=3,p=4$8UjK8e2GJL2hC7yRi0GRNg$XtdtCN3GNDUPH3YWBAyqyEXXOvQJfXvCcAmOVOEd3Ww'),
    ('support', '3', 'support2', 3, '$argon2id$v=19$m=65536,t=3,p=4$8UjK8e2GJL2hC7yRi0GRNg$XtdtCN3GNDUPH3YWBAyqyEXXOvQJfXvCcAmOVOEd3Ww');

INSERT INTO client (`first_name`, `last_name`, `email`, `telephone`, `company_name`, `commercial_id`)
VALUES
    ('premier', 'client', 'mail1', '0666666666', 'company1', 2);

INSERT INTO contract (`client_id`, `total_amount`, `due_amount`, `status`)
VALUES
    ('1', 56.55, 5.5, 'signed'),
    ('1', 645.66, 645.66, 'to_be_signed'),
    ('1', 35.00, 0.00, 'signed');

INSERT INTO event (`contract_id`, `client_id`, `start_date`, `end_date`, `support_contact_id`, `location`, `attendees_number`, `notes`)
VALUES
    (1, 1, '25/05/2023', '29/09/2023', 3, 'Paris', 50, null),
    (2, 1, '25/05/2023', '29/09/2023', null, 'Paris', 50, null),
    (3, 1, '25/05/2023', '29/09/2023', 3, 'Paris', 50, 'fini');
