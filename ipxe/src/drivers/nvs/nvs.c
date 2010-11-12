/*
 * Copyright (C) 2006 Michael Brown <mbrown@fensystems.co.uk>.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of the
 * License, or any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

FILE_LICENCE ( GPL2_OR_LATER );

#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <assert.h>
#include <ipxe/nvs.h>

/** @file
 *
 * Non-volatile storage
 *
 */

/**
 * Read from non-volatile storage device
 *
 * @v nvs		NVS device
 * @v address		Address from which to read
 * @v data		Data buffer
 * @v len		Length of data buffer
 * @ret rc		Return status code
 */
int nvs_read ( struct nvs_device *nvs, unsigned int address,
	       void *data, size_t len ) {
	size_t frag_len;
	int rc;

	/* We don't even attempt to handle buffer lengths that aren't
	 * an integral number of words.
	 */
	assert ( ( len & ( ( 1 << nvs->word_len_log2 ) - 1 ) ) == 0 );

	while ( len ) {

		/* Calculate space remaining up to next block boundary */
		frag_len = ( ( nvs->block_size -
			       ( address & ( nvs->block_size - 1 ) ) )
			     << nvs->word_len_log2 );

		/* Limit to space remaining in buffer */
		if ( frag_len > len )
			frag_len = len;

		/* Read this portion of the buffer from the device */
		if ( ( rc = nvs->read ( nvs, address, data, frag_len ) ) != 0 )
			return rc;

		/* Update parameters */
		data += frag_len;
		address += ( frag_len >> nvs->word_len_log2 );
		len -= frag_len;
	}

	return 0;
}

/**
 * Verify content of non-volatile storage device
 *
 * @v nvs		NVS device
 * @v address		Address from which to read
 * @v data		Data to compare against
 * @v len		Length of data buffer
 * @ret rc		Return status code
 */
static int nvs_verify ( struct nvs_device *nvs, unsigned int address,
			const void *data, size_t len ) {
	uint8_t read_data[len];
	int rc;

	/* Read data into temporary buffer */
	if ( ( rc = nvs_read ( nvs, address, read_data, len ) ) != 0 )
		return rc;

	/* Compare data */
	if ( memcmp ( data, read_data, len ) != 0 ) {
		DBG ( "NVS %p verification failed at %#04x+%zd\n",
		      nvs, address, len );
		return -EIO;
	}

	return 0;
}

/**
 * Write to non-volatile storage device
 *
 * @v nvs		NVS device
 * @v address		Address to which to write
 * @v data		Data buffer
 * @v len		Length of data buffer
 * @ret rc		Return status code
 */
int nvs_write ( struct nvs_device *nvs, unsigned int address,
		const void *data, size_t len ) {
	size_t frag_len;
	int rc;

	/* We don't even attempt to handle buffer lengths that aren't
	 * an integral number of words.
	 */
	assert ( ( len & ( ( 1 << nvs->word_len_log2 ) - 1 ) ) == 0 );

	while ( len ) {

		/* Calculate space remaining up to next block boundary */
		frag_len = ( ( nvs->block_size -
			       ( address & ( nvs->block_size - 1 ) ) )
			     << nvs->word_len_log2 );

		/* Limit to space remaining in buffer */
		if ( frag_len > len )
			frag_len = len;

		/* Write this portion of the buffer to the device */
		if ( ( rc = nvs->write ( nvs, address, data, frag_len ) ) != 0)
			return rc;

		/* Read back and verify data */
		if ( ( rc = nvs_verify ( nvs, address, data, frag_len ) ) != 0)
			return rc;

		/* Update parameters */
		data += frag_len;
		address += ( frag_len >> nvs->word_len_log2 );
		len -= frag_len;
	}

	return 0;
}
