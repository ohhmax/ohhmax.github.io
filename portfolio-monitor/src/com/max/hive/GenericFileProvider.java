package com.max.hive;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.net.Uri;
import android.os.ParcelFileDescriptor;
import android.provider.OpenableColumns;
import android.webkit.MimeTypeMap;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Locale;

/**
 * MaxHive GenericFileProvider
 * Pure standard Android framework ContentProvider.
 * Provides content:// URIs for external viewing and sharing without external AndroidX dependencies.
 */
public class GenericFileProvider extends ContentProvider {
    public static final String AUTHORITY = "com.max.hive.fileprovider";
    private static final String[] DEFAULT_COLUMNS = new String[] {
        OpenableColumns.DISPLAY_NAME,
        OpenableColumns.SIZE
    };

    @Override
    public boolean onCreate() {
        return true;
    }

    public static Uri getUriForFile(Context context, File file) {
        if (file == null) return null;
        return new Uri.Builder()
            .scheme("content")
            .authority(AUTHORITY)
            .appendPath(file.getName())
            .build();
    }

    private File resolveFile(String filename) {
        Context ctx = getContext();
        if (ctx == null || filename == null) return null;

        // Strip path traversal attempts
        String safeName = new File(filename).getName();

        // 1. External files downloads dir
        File extDownloads = ctx.getExternalFilesDir("downloads");
        if (extDownloads != null) {
            File f = new File(extDownloads, safeName);
            if (f.exists()) return f;
        }

        // 2. Cache attachments dir
        File cacheAtts = new File(ctx.getCacheDir(), "attachments");
        File fCacheAtts = new File(cacheAtts, safeName);
        if (fCacheAtts.exists()) return fCacheAtts;

        // 3. Cache root dir
        File fCache = new File(ctx.getCacheDir(), safeName);
        if (fCache.exists()) return fCache;

        // 4. Internal files dir
        File fFiles = new File(ctx.getFilesDir(), safeName);
        if (fFiles.exists()) return fFiles;

        // Default to downloads location for potential incoming creation
        return extDownloads != null ? new File(extDownloads, safeName) : new File(ctx.getCacheDir(), safeName);
    }

    @Override
    public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException {
        String filename = uri.getLastPathSegment();
        if (filename == null) {
            throw new FileNotFoundException("Invalid URI: " + uri);
        }

        File target = resolveFile(filename);
        if (target == null || !target.exists()) {
            throw new FileNotFoundException("File not found on device: " + filename);
        }

        int fileMode = ParcelFileDescriptor.MODE_READ_ONLY;
        if ("w".equalsIgnoreCase(mode) || "wt".equalsIgnoreCase(mode)) {
            fileMode = ParcelFileDescriptor.MODE_WRITE_ONLY;
        } else if ("rw".equalsIgnoreCase(mode) || "rwt".equalsIgnoreCase(mode)) {
            fileMode = ParcelFileDescriptor.MODE_READ_WRITE;
        }

        return ParcelFileDescriptor.open(target, fileMode);
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {
        if (projection == null) {
            projection = DEFAULT_COLUMNS;
        }

        String filename = uri.getLastPathSegment();
        File file = (filename != null) ? resolveFile(filename) : null;

        MatrixCursor cursor = new MatrixCursor(projection);
        Object[] values = new Object[projection.length];

        for (int i = 0; i < projection.length; i++) {
            String col = projection[i];
            if (OpenableColumns.DISPLAY_NAME.equals(col)) {
                values[i] = (file != null && file.exists()) ? file.getName() : filename;
            } else if (OpenableColumns.SIZE.equals(col)) {
                values[i] = (file != null && file.exists()) ? file.length() : 0L;
            } else {
                values[i] = null;
            }
        }

        cursor.addRow(values);
        return cursor;
    }

    @Override
    public String getType(Uri uri) {
        String filename = uri.getLastPathSegment();
        if (filename == null) return "application/octet-stream";

        int dot = filename.lastIndexOf('.');
        if (dot >= 0) {
            String ext = filename.substring(dot + 1).toLowerCase(Locale.US);
            String mime = MimeTypeMap.getSingleton().getMimeTypeFromExtension(ext);
            if (mime != null && !mime.isEmpty()) {
                return mime;
            }
            if ("apk".equals(ext)) return "application/vnd.android.package-archive";
            if ("json".equals(ext)) return "application/json";
            if ("log".equals(ext)) return "text/plain";
            if ("csv".equals(ext)) return "text/csv";
            if ("pdf".equals(ext)) return "application/pdf";
            if ("zip".equals(ext)) return "application/zip";
        }
        return "application/octet-stream";
    }

    @Override
    public Uri insert(Uri uri, ContentValues values) {
        return null;
    }

    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        return 0;
    }

    @Override
    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
        return 0;
    }
}
