import { db } from '../db';
import bcrypt from 'bcrypt';

export const create = async (user: any) => {
    const { name, email, password, address, phone, interestedCategories, interestedTags } = user;

    // Hash the password before saving
    const hashedPassword = await bcrypt.hash(password, 10);

    return db.one('INSERT INTO users(name, email, password, address, phone, interested_categories, interested_tags) VALUES($1, $2, $3, $4, $5, $6, $7) RETURNING *',
        [name, email, hashedPassword, address, phone, interestedCategories, interestedTags]);
};

export const findAll = async () => {
    return db.any('SELECT * FROM users');
};

export const findById = async (id: string) => {
    return db.oneOrNone('SELECT * FROM users WHERE id = $1', [id]);
};

export const findByEmail = async (email: string) => {
  return db.oneOrNone('SELECT * FROM users WHERE email = $1', [email]);
};

export const update = async (id: string, user: any) => {
    const { name, email, password, address, phone, interestedCategories, interestedTags } = user;
    return db.oneOrNone('UPDATE users SET name = $1, email = $2, password = $3, address = $4, phone = $5, interested_categories = $6, interested_tags = $7 WHERE id = $8 RETURNING *',
        [name, email, password, address, phone, interestedCategories, interestedTags, id]);
};

export const remove = async (id: string) => {
    return db.result('DELETE FROM users WHERE id = $1', [id]);
};
